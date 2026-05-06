import { httpService } from '../services/http.service.js'
export class BaseModal {
    constructor(htmlPath, cssPath, modalId, onCloseCallback) {
        this.onCloseCallback = onCloseCallback;
        this.htmlPath = htmlPath;
        this.cssPath = cssPath;
        this.modalId = modalId;

        this.modalElement = null;
        this.bootstrapModal = null;
        this.jqueryElement = null;
        this.isInitialized = false;
        this.modalContainer = $('#modalContainer');
    }

    loadStyles() {
        if (this.cssPath && !$(`link[href="${this.cssPath}"]`).length) {
            const link = $('<link />').attr('rel', 'stylesheet').attr('href', this.cssPath);
            $('head').append(link);
        }
    }

    async renderModal() {
        const modalHtml = await httpService.get(this.htmlPath);
        this.removeModalElementIfExists();
        this.modalContainer.append(modalHtml);
        this.modalElement = document.getElementById(this.modalId);
        this.jqueryElement = $(this.modalElement);
        this.bootstrapModal = new bootstrap.Modal(this.modalElement);

        this.modalElement.addEventListener('hide.bs.modal', () => {
            if (this.modalElement.contains(document.activeElement)) {
                document.activeElement.blur();
            }
            this.modalElement.remove();
        }, { once: true });
    }

    async init() {
        this.isInitialized = true;
        this.loadStyles();
        await this.renderModal();
        this.addEventHandlers();
    }
    
    removeModalElementIfExists() {
        this.modalElement = document.getElementById(this.modalId);
        if (this.modalElement) {
            this.modalElement.remove();
        }
        this.modalElement = null;
    }

    addEventHandlers() {
        // To be overrode by child class
    }

    prefillData(data) {
        // To be overrode by child class
    }

    close(data) {
        this.onCloseCallback(data);
        this.hide();
    }

    async show(data) {
        if (!this.isInitialized) {
            await this.init();
        }
        if (data) {
            this.prefillData(data);
        }
        this.bootstrapModal.show();
    }

    hide() {
        this.bootstrapModal.hide();
    }
}