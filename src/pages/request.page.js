import { RequestModal } from "../modals/request.modal.js";
import { service } from "../services/data.service.js";
class RequestPage {
    constructor(container, params) {
        this.container = container;
        this.params = params;
        this.request = null;
    }

    async render() {
        this.request = await service.findRequestById(Number(this.params.requestId));
        this.container.html(await this.template())  ;
        this.onInit();
    }

    onInit() {
        this.fillDataValue('.request', {
            request: this.request
        });

        $("#offering-skills").html(
            this.request.offering.skills.map(skill => $('<div></div>').addClass('skill-chip').text(skill.name))
        );

        $(".request-status").addClass(`status-${this.request.status.toLowerCase()}`)

        $.get('src/components/offer.component.html').then(offerHtml => {
            this.request.offers.forEach((offer) => {
                const offerer = offer.offerer;
                $('#offers').append(this.fillDataValue(offerHtml, offerer));
            });
        });

        $("#btn-edit-request").click(() => {
            const requestModal = new RequestModal((data) => {
                console.log(data);
            });
            requestModal.show(this.request);
        })
    }

    template() {
        return $.get(`src/pages/request.page.html`);
    }

    fetchData(obj, path) {
        if (path.length === 0 || typeof (obj) !== typeof ({})) {
            return obj;
        }
        const [field, ...rest] = path;
        return this.fetchData(obj[field], rest);
    }

    fillDataValue(elementHtml, obj) {
        const element = $(elementHtml);
        element.find('[app-data-value]').get().forEach(element => {
            const value = this.fetchData(obj, $(element).attr('app-data-value').split('.'));
            $(element).text(value);
        });
        element.find('[app-attr-value]').get().forEach(childElement => {
            const appAttrValue = $(childElement).attr('app-attr-value').split(',');
            appAttrValue.forEach(attrName => {
                $(childElement).attr(attrName, format($(childElement).attr(attrName), obj));
            });
        })
        return element;
    }

    format(template, data) {
        return template.replace(/{{([^}]+)}}/g, (match, key) => {
            return this.fetchData(data, key.split('.'));
        });
    }
}

export const Page = RequestPage;