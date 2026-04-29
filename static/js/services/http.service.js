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
}

export const httpService = new HttpService(); 