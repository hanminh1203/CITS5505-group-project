class HttpService {
    spinnerElement = null;
    constructor() {
        this.spinnerElement = $('#spinner');
    }
    get(url) {
        return this.displaySpinner($.get(url));
    }

    post(csrfToken, url, data) {
        return this.displaySpinner(this.doPost(csrfToken, url, data));
    }

    async doPost(csrfToken, url, data) {
        try {
            return await $.ajax({
                url,
                type: 'POST',
                headers: { 'X-CSRF-Token': csrfToken },
                data
            });
        } catch (error) {
            if (!error.responseJSON?.expected) {
                // lazy import to avoid circular dependency between http.service and error.modal
                const { ErrorModal } = await import("../modals/error.modal.js");
                new ErrorModal("An error occurred while processing your request. Please try again later.",
                    error.responseJSON?.stacktrace).show();
            }
            throw error;
        }
    }

    delete(csrfToken, url) {
        return this.displaySpinner(this.doDelete(csrfToken, url))
    }

    async doDelete(csrfToken, url) {
        try {
            return await $.ajax({
                url,
                type: 'DELETE',
                headers: { 'X-CSRF-Token': csrfToken }
            });
        } catch (error) {
            if (!error.responseJSON?.expected) {
                // lazy import to avoid circular dependency between http.service and error.modal
                const { ErrorModal } = await import("../modals/error.modal.js");
                new ErrorModal("An error occurred while processing your request. Please try again later.",
                    error.responseJSON?.stacktrace).show();
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