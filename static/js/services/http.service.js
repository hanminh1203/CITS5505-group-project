class HttpService {
    spinnerElement = null;
    constructor() {
        this.spinnerElement = $('#spinner');
    }
    get(url) {
        return this.displaySpinner(this.request({ url, type: 'GET' }));
    }

    post(csrfToken, url, data) {
        return this.displaySpinner(this.request({
            url,
            type: 'POST',
            headers: { 'X-CSRF-Token': csrfToken },
            data
        }));
    }

    put(csrfToken, url, data) {
        return this.displaySpinner(this.request({
            url,
            type: 'PUT',
            headers: { 'X-CSRF-Token': csrfToken },
            data
        }));
    }

    delete(csrfToken, url) {
        return this.displaySpinner(this.request({
            url,
            type: 'DELETE',
            headers: { 'X-CSRF-Token': csrfToken }
        }));
    }

    async request(options) {
        try {
            return await $.ajax(options);
        } catch (error) {
            if (!error.responseJSON?.expected) {
                const message = error.responseJSON?.message ||
                    "An error occurred while processing your request. Please try again later.";
                // lazy import to avoid circular dependency between http.service and error.modal
                const { ErrorModal } = await import("../modals/error.modal.js");
                new ErrorModal(message, error.responseJSON?.stacktrace).show();
            }
            throw error;
        }
    }

    async displaySpinner(promise) {
        try {
            this.spinnerElement.show();
            return await promise;
        } finally {
            this.spinnerElement.hide();
        }
    }
}

export const httpService = new HttpService(); 