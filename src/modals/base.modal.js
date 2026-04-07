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
    }

    #loadStyles() {
        if (this.cssPath && !$(`link[href="${this.cssPath}"]`).length) {
            const link = $('<link />').attr('rel', 'stylesheet').attr('href', this.cssPath);
            $('head').append(link);
        }
    }

    async #renderModal() {
        const modalHtml = await $.get(this.htmlPath);
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        this.modalElement = document.getElementById(this.modalId);
        this.jqueryElement = $(this.modalElement);
        this.bootstrapModal = new bootstrap.Modal(this.modalElement);
    }

    async #init() {
        this.isInitialized = true;
        this.#loadStyles();
        await this.#renderModal();
        this.addEventHandlers();
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
            await this.#init();
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