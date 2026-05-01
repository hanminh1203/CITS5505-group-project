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
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        this.modalElement = document.getElementById(this.modalId);
        this.jqueryElement = $(this.modalElement);
        this.bootstrapModal = new bootstrap.Modal(this.modalElement);
        this.modalBackdrop = null;

        this.modalElement.addEventListener('show.bs.modal', () => {
            // Calculate z-index based on the number of currently open modals
            // so the new modal would on top of the existing ones
            const countOfModal = $('.modal').length;
            this.modalBackdrop = $('.modal-backdrop:not(.z-index-set)').first();
            this.modalBackdrop.addClass('z-index-set');
            this.modalBackdrop.css('z-index', 1050 + countOfModal * 10);
            this.jqueryElement.css('z-index', 1050 + countOfModal * 10 + 1);
        });

        this.modalElement.addEventListener('hide.bs.modal', () => {
            if (this.modalElement.contains(document.activeElement)) {
                document.activeElement.blur();
            }
            this.modalElement.remove();
            if (this.modalBackdrop) {
                this.modalBackdrop.remove();
            }
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
        if (this.onCloseCallback) {
            this.onCloseCallback(data);
        }
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