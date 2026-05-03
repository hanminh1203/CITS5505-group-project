class HttpService {
    get(url) {
        return $.get(url);
    }

    post(csrfToken, url, data) {
        return $.ajax({
            url,
            type: 'POST',
            headers: { 'X-CSRF-Token': csrfToken },
            data
        });
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