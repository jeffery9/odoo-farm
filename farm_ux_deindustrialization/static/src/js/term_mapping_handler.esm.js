/** @odoo-module **/

import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils";
import { registry } from "@web/core/registry";

/**
 * TermMappingHandler - 术语映射处理器组件
 * 
 * 此组件负责在前端动态替换术语，将工业术语替换为农业术语
 */
export class TermMappingHandler extends Component {
    /**
     * 组件设置方法
     */
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            termMappings: [],
            loaded: false
        });
        
        onWillStart(async () => {
            await this.loadTermMappings();
        });
        
        onMounted(() => {
            if (this.state.loaded) {
                this.applyTermMappingsToPage();
                this.watchDOMChanges();
            }
        });
    }

    /**
     * 加载术语映射
     */
    async loadTermMappings() {
        try {
            // 从后端获取术语映射
            const termMappings = await this.orm.searchRead(
                'term.mapping',
                [['is_active', '=', true]],
                ['source_term', 'target_term']
            );
            
            this.state.termMappings = termMappings || [];
            this.state.loaded = true;
            
            if (this.state.termMappings.length > 0) {
                this.applyTermMappingsToPage();
                this.watchDOMChanges();
            }
        } catch (error) {
            console.error('Error loading term mappings:', error);
        }
    }

    /**
     * 应用术语映射到页面
     */
    applyTermMappingsToPage() {
        if (!this.state.termMappings || this.state.termMappings.length === 0) {
            return;
        }

        // 替换页面中的文本节点
        this.replaceTextInDOM(document.body);
    }

    /**
     * 在DOM元素中替换文本
     * @param {HTMLElement} element - DOM元素
     */
    replaceTextInDOM(element) {
        if (!this.state.termMappings || this.state.termMappings.length === 0) {
            return;
        }

        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.parentElement && 
                !['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT'].includes(node.parentElement.tagName) &&
                node.nodeValue.trim() !== '') {
                textNodes.push(node);
            }
        }

        // 按长度排序，优先替换较长的术语
        const sortedMappings = [...this.state.termMappings].sort((a, b) => 
            (b.source_term || "").length - (a.source_term || "").length
        );

        textNodes.forEach(textNode => {
            let originalText = textNode.nodeValue;
            let newText = originalText;

            sortedMappings.forEach(mapping => {
                if (mapping.source_term && mapping.target_term) {
                    // 使用正则表达式进行全局、不区分大小写的替换
                    const regex = new RegExp(this.escapeRegExp(mapping.source_term), 'gi');
                    newText = newText.replace(regex, mapping.target_term);
                }
            });

            if (newText !== originalText) {
                textNode.nodeValue = newText;
            }
        });
    }

    /**
     * 转义正则表达式特殊字符
     * @param {string} string - 需要转义的字符串
     * @returns {string} 转义后的字符串
     */
    escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\\]/g, '\\$&');
    }

    /**
     * 监听DOM变化
     */
    watchDOMChanges() {
        if (!this.state.termMappings || this.state.termMappings.length === 0) {
            return;
        }

        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            setTimeout(() => {
                                this.replaceTextInDOM(node);
                            }, 0);
                        } else if (node.nodeType === Node.TEXT_NODE) {
                            const parentElement = node.parentElement;
                            if (parentElement && 
                                !['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT'].includes(parentElement.tagName)) {
                                this.replaceTextInDOM(parentElement);
                            }
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    static template = 'TermMappingHandler';
}

registry.category("main_components").add("TermMappingHandler", { Component: TermMappingHandler });
