const {createApp, ref, computed, onMounted, watch, nextTick} = Vue;

const LinkItem = {
    name: 'LinkItem',
    props: ['link', 'category', 'depth'],
    template: `
        <li class="link-item">
            <div class="link-title" @click="$emit('open-modal', link, category)">
                <div class="link-content">
                    <span class="link-title-text">{{ link.title }}</span>
                </div>
                <div class="link-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>

            <ul v-if="link.child && link.child.length > 0" class="child-links">
                <link-item
                    v-for="(child, childIndex) in link.child"
                    :key="'child-' + depth + '-' + childIndex"
                    :link="child"
                    :category="category"
                    :depth="depth + 1"
                    @open-modal="$emit('open-modal', child, category)"
                />
            </ul>
        </li>
    `
};

createApp({
    components: {
        LinkItem
    },
    setup() {
        const linksData = ref(LINKS);
        const showModal = ref(false);
        const selectedDir = ref(localStorage.getItem('selectedDir'));
        const markdownContent = ref('');
        const currentModalTitle = ref('');
        const loading = ref(false);
        const currentLink = ref(null);
        const currentCategory = ref(null);
        const modalContentRef = ref(null);

        // Инициализация highlight.js
        const initHighlight = () => {
            if (window.hljs) {
                hljs.configure({
                    languages: ['python', 'go']
                });
            }
        };

        // Подсветка кода в модальном окне
        const highlightCodeBlocks = () => {
            if (!modalContentRef.value || !window.hljs) return;

            nextTick(() => {
                const codeBlocks = modalContentRef.value.querySelectorAll('pre code');
                codeBlocks.forEach((block) => {
                    // Если блок уже подсвечен - пропускаем
                    if (block.classList.contains('hljs')) {
                        return;
                    }
                    hljs.highlightElement(block);
                });
            });
        };

        // Настройка marked.js с подсветкой синтаксиса
        marked.setOptions({
            highlight: function(code, lang) {
                if (window.hljs) {
                    // Нормализация названий языков
                    if (lang === 'golang') lang = 'go';
                    if (lang === 'py') lang = 'python';

                    if (lang && hljs.getLanguage(lang)) {
                        try {
                            return hljs.highlight(code, {
                                language: lang,
                                ignoreIllegals: true
                            }).value;
                        } catch (err) {
                            console.warn(`Ошибка подсветки для языка ${lang}:`, err);
                            return hljs.highlightAuto(code).value;
                        }
                    }
                    return hljs.highlightAuto(code).value;
                }
                return code; // Если hljs не загружен, возвращаем код как есть
            },
            langPrefix: 'hljs language-'
        });

        const extractMarkdownSection = (content, uri) => {
            if (!content || !uri) return '';

            // Fix image folder patch
            content = content.replaceAll('../images', '/notes/images');

            const lines = content.split('\n');
            const targetHeading = uri.trim();

            let startIndex = -1;
            let inCodeBlock = false;
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].includes('```')) {
                    inCodeBlock = !inCodeBlock;
                    continue;
                }
                if (inCodeBlock) continue;

                if (lines[i].trim() === targetHeading) {
                    startIndex = i;
                    break;
                }
            }

            if (startIndex === -1) {
                inCodeBlock = false;
                for (let i = 0; i < lines.length; i++) {
                    if (lines[i].includes('```')) {
                        inCodeBlock = !inCodeBlock;
                        continue;
                    }
                    if (inCodeBlock) continue;

                    const line = lines[i].trim();
                    if (line.includes(targetHeading.replace('#', '').trim())) {
                        startIndex = i;
                        break;
                    }
                }
            }

            if (startIndex === -1) return '';

            const targetLevel = targetHeading.match(/^#+/)[0].length;

            let endIndex = lines.length;
            inCodeBlock = false;
            for (let i = startIndex + 1; i < lines.length; i++) {
                if (lines[i].includes('```')) {
                    inCodeBlock = !inCodeBlock;
                    continue;
                }
                if (inCodeBlock) continue;

                const line = lines[i].trim();
                if (line.startsWith('#')) {
                    const level = line.match(/^#+/)[0].length;
                    if (level <= targetLevel) {
                        endIndex = i;
                        break;
                    }
                }
            }

            return lines.slice(startIndex, endIndex).join('\n');
        };

        const openModal = async (link, category) => {
            currentLink.value = link;
            currentCategory.value = category;
            currentModalTitle.value = link.title;
            showModal.value = true;
            loading.value = true;
            markdownContent.value = '';

            try {
                const dir = linksData.value[selectedDir.value].dir;
                const filePath = `./notes/${dir}/${link.file}`;
                const response = await fetch(filePath);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const content = await response.text();
                const extractedContent = extractMarkdownSection(content, link.uri);

                if (!extractedContent) {
                    markdownContent.value = `## ${link.title}\n\nСодержимое для этого раздела не найдено в файле.`;
                } else {
                    markdownContent.value = extractedContent;
                }
            } catch (error) {
                console.error('Error loading markdown:', error);
                markdownContent.value = `# Ошибка\n\nНе удалось загрузить файл: ${link.file}\n\n\`${error.message}\``;
            } finally {
                loading.value = false;
            }
        };

        const closeModal = () => {
            showModal.value = false;
            markdownContent.value = '';
            currentLink.value = null;
            currentCategory.value = null;
        };

        const chooseDir = (dirIndex) => {
            if (dirIndex === null) {
                localStorage.removeItem('selectedDir');
            } else {
                localStorage.setItem('selectedDir', dirIndex);
            }
            selectedDir.value = dirIndex;
        };

        const renderedMarkdown = computed(() => {
            if (!markdownContent.value) return '';
            const html = marked.parse(markdownContent.value);

            // Вызываем подсветку после рендеринга
            highlightCodeBlocks();

            return html;
        });

        const totalCategories = computed(() => {
            return linksData.value.length;
        });

        const linksDataByDir = (currentDir) => {
            return computed(() => linksData.value[currentDir])
        }

        const currentDirName = () => {
            return selectedDir.value ? linksData.value[selectedDir.value].dir : '';
        }

        const totalLinks = computed(() => {
            let count = 0;
            const countLinks = (items) => {
                items.forEach(item => {
                    count++;
                    if (item.child && item.child.length > 0) {
                        countLinks(item.child);
                    }
                });
            };

            linksData.value.forEach(category => {
                if (category.links) {
                    countLinks(category.links);
                }
            });

            return count;
        });

        const totalFiles = computed(() => {
            let total = 0;
            linksData.value.forEach(category => {
                total += category.links.length;
            });

            return total;
        });

        // Инициализация при монтировании
        onMounted(() => {
            initHighlight();
        });

        // Обновляем подсветку при изменении контента
        watch([showModal, markdownContent], () => {
            if (showModal.value && markdownContent.value) {
                highlightCodeBlocks();
            }
        });

        return {
            linksData,
            showModal,
            selectedDir,
            markdownContent,
            currentModalTitle,
            loading,
            currentLink,
            currentCategory,
            renderedMarkdown,
            totalCategories,
            totalLinks,
            totalFiles,
            currentDirName,
            linksDataByDir,
            openModal,
            closeModal,
            chooseDir,
            modalContentRef,
            highlightCodeBlocks
        };
    }
}).mount('#app');