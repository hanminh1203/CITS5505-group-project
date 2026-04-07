import { BaseModal } from "./base.modal.js";

export class RequestModal extends BaseModal {
    constructor(onSaveCallback) {
        super('src/modals/request.modal.html', null, 'request-modal', onSaveCallback);
        this.data = null;
    }
    
    addEventHandlers() {
        const form = this.modalElement.querySelector('#request-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.#onSubmit(e.target);
        });
    }

    #onSubmit(form) {
        const data = $(form).serializeArray()
            .reduce((values, x) => {
                values[x.name] = x.value;
                return values;
            }, {});
        this.close({
            ...this.data,
            ...data,
        });
    }

    prefillData(data) {
        this.data = data;
        this.jqueryElement.find('#request-name').val(data.name);
        this.jqueryElement.find('#request-description').val(data.description);
        this.jqueryElement.find('#request-session-format').val(data.format);
        this.jqueryElement.find('#request-duration').val(data.duration);
        this.jqueryElement.find('#request-availability').val(data.availability);
    }
}