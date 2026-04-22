class HttpService {
    get(url) {
        return $.get(url);
    }

    post(csrfToken, url, data) {
        return $.post(url, data);
    }
}

export const httpService = new HttpService(); 