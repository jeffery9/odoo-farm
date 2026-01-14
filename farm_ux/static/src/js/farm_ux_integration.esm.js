/** @odoo-module **/

import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils";
import { registry } from "@web/core/registry";
import { session } from "@web/session";

/**
 * FarmUXIntegration - 农场用户体验集成组件
 */
export class FarmUXIntegration extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            workspaceCustomization: {},
            visualIndicators: [],
            accessibilityFeatures: {},
            contextualHelp: [],
            weatherData: null,
            activeTab: 'knowledge',
            showHelpPanel: false,
            currentModel: '',
            currentViewType: '',
            loaded: false
        });

        onWillStart(async () => {
            await this.loadAllCustomizations();
        });

        onMounted(() => {
            this.applyAllCustomizations();
            this.watchDOMChanges();
            this.listenToViewChanges();
        });
    }

    async loadAllCustomizations() {
        try {
            const customization = session.workspace_customization || await this.orm.call(
                'workspace.customization', 'get_user_customization', [[]], { user_id: this.env.session.uid }
            );

            const visualIndicators = await this.orm.searchRead(
                'visual.status.indicator', [['is_active', '=', true]],
                ['id', 'status_type', 'status_value', 'color_code', 'icon_class', 'badge_style']
            );

            const accessibilityFeatures = session.accessibility_features || await this.orm.call(
                'accessibility.integration', 'get_accessibility_features', [[]], { user_id: this.env.session.uid }
            );

            Object.assign(this.state, {
                workspaceCustomization: customization || {},
                visualIndicators: visualIndicators || [],
                accessibilityFeatures: accessibilityFeatures || {},
                loaded: true
            });
        } catch (error) {
            console.error('Error loading customizations:', error);
        }
    }

    applyAllCustomizations() {
        if (!this.state.loaded) return;
        this.applyTheme(this.state.workspaceCustomization.theme);
        this.applyFontSize(this.state.workspaceCustomization.font_size);
        this.applyAccessibilityFeatures(this.state.accessibilityFeatures);
        this.applyVisualStatusIndicatorsToElements();
    }

    applyTheme(theme) {
        if (!theme) return;
        document.body.classList.remove('workspace-theme-dark', 'workspace-theme-eye-care', 'workspace-theme-high-contrast');
        if (theme !== 'light') document.body.classList.add(`workspace-theme-${theme}`);
    }

    applyFontSize(fontSize) {
        if (!fontSize) return;
        document.body.classList.remove('font-size-small', 'font-size-normal', 'font-size-large', 'font-size-extra-large');
        document.body.classList.add(`font-size-${fontSize}`);
    }

    applyAccessibilityFeatures(features) {
        if (!features) return;
        if (features.high_contrast_mode) document.body.classList.add('accessibility-high-contrast');
        if (features.larger_text_size) document.body.classList.add('accessibility-larger-text');
        if (features.reduced_motion) document.body.classList.add('reduce-motion');
        if (features.screen_reader_enabled) this.enableScreenReaderCompatibility();
    }

    /**
     * 监听视图变化以获取上下文帮助和天气
     */
    listenToViewChanges() {
        const self = this;
        // 在 Odoo 19 中，我们可以监听控制器变化
        // 这里简化为定时检查或通过 toggleHelpPanel 触发
    }

    /**
     * 加载上下文数据 (帮助、天气等)
     */
    async loadContextData(model, viewType, resId) {
        if (!model) return;
        try {
            // 1. 加载上下文帮助
            const helpData = await this.orm.call(
                'accessibility.integration',
                'get_contextual_help_data',
                [],
                { model_name: model, view_type: viewType }
            );
            this.state.contextualHelp = helpData;

            // 2. 加载天气 (如果是干预或地块相关)
            if (resId && (model === 'mrp.production' || model === 'project.task' || model === 'stock.location')) {
                const weatherData = await this.orm.call(
                    'farm.weather.forecast',
                    'get_context_weather',
                    [],
                    { res_model: model, res_id: resId }
                );
                this.state.weatherData = weatherData;
            } else {
                this.state.weatherData = null;
            }

            this.state.currentModel = model;
            this.state.currentViewType = viewType;
        } catch (error) {
            console.error('Error loading context data:', error);
        }
    }

    toggleHelpPanel() {
        this.state.showHelpPanel = !this.state.showHelpPanel;
        if (this.state.showHelpPanel) {
            // 从当前控制器获取模型信息
            const controller = this.action.currentController;
            if (controller && controller.props.resModel) {
                this.loadContextData(
                    controller.props.resModel, 
                    controller.props.type || 'form',
                    controller.props.resId
                );
            }
        }
    }

    /**
     * 语音控制集成 [US-16-07]
     */
    startVoiceControl() {
        if (!('webkitSpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            return;
        }

        const recognition = new window.webkitSpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onresult = (event) => {
            const command = event.results[0][0].transcript;
            this.processVoiceCommand(command);
        };

        recognition.start();
    }

    processVoiceCommand(command) {
        console.log('Voice Command received:', command);
        if (command.includes('开始') || command.includes('作业')) {
            const btn = document.querySelector('.o_agri_action_buttons .btn-success');
            if (btn) btn.click();
        } else if (command.includes('停止') || command.includes('结束')) {
            const btn = document.querySelector('.o_agri_action_buttons .btn-warning');
            if (btn) btn.click();
        } else if (command.includes('完成') || command.includes('保存')) {
            const btn = document.querySelector('.o_form_button_save, .o_agri_action_buttons .btn-primary');
            if (btn) btn.click();
        }
    }



    enableScreenReaderCompatibility() {
        const elements = document.querySelectorAll('button, a, input, select, textarea');
        elements.forEach(el => {
            if (!el.getAttribute('aria-label') && !el.title) {
                const text = el.textContent.trim() || el.value || el.placeholder || '';
                if (text) el.setAttribute('aria-label', text);
            }
        });
    }

    applyVisualStatusIndicatorsToElements() {
        if (!this.state.visualIndicators || this.state.visualIndicators.length === 0) return;
        this.state.visualIndicators.forEach(indicator => {
            const selector = `[data-status-type="${indicator.status_type}"][data-status-value="${indicator.status_value}"]`;
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (el.querySelector(`.visual-status-indicator[data-id="${indicator.id}"]`)) return;
                const indicatorEl = document.createElement('span');
                indicatorEl.className = `visual-status-indicator badge rounded-pill bg-${indicator.badge_style || 'secondary'} ms-1`;
                indicatorEl.dataset.id = indicator.id;
                if (indicator.color_code) indicatorEl.style.backgroundColor = indicator.color_code;
                if (indicator.icon_class) {
                    const iconEl = document.createElement('i');
                    iconEl.className = indicator.icon_class;
                    indicatorEl.appendChild(iconEl);
                }
                el.appendChild(indicatorEl);
            });
        });
    }

    watchDOMChanges() {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    setTimeout(() => {
                        this.applyVisualStatusIndicatorsToElements();
                    }, 100);
                }
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }

    static template = 'FarmUXIntegration';
}

registry.category("main_components").add("FarmUXIntegration", { Component: FarmUXIntegration });
