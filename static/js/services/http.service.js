class HttpService {
    get(url) {
        return $.get(url);
    }

    async post(csrfToken, url, data) {
        try {
        return await $.ajax({
            url,
            type: 'POST',
            headers: { 'X-CSRF-Token': csrfToken },
            data
        });
        } catch (error) {
            // lazy import to avoid circular dependency between http.service and error.modal
            const { ErrorModal } = await import ("../modals/error.modal.js");
            const errorModal = new ErrorModal("An error occurred while processing your request. Please try again later.",
                error.responseJSON?.stacktrace).show();
            errorModal.show();
            throw error;
        }
    }

    delete(csrfToken, url) {
        return $.ajax({
            url,
            type: 'DELETE',
            headers: { 'X-CSRF-Token': csrfToken }
        });
    }
}

export const httpService = new HttpService(); 