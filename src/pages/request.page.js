import { RequestModal } from "../modals/request.modal.js";
import { OfferModal } from "../modals/offer.modal.js";
import { service } from "../services/data.service.js";
class RequestPage {
    constructor(container, params) {
        this.container = container;
        this.params = params;
        this.request = null;
        this.templates = {
            offer: null
        };
    }

    async render() {
        this.request = await service.findRequestById(Number(this.params.requestId));
        if (!this.request) {
            window.location.hash = '404';
            return;
        }

        this.templates.offer = await $.get('src/components/offer.component.html');
        this.container.html(await this.#template());
        this.#onInit();
    }

    #onInit() {
        this.#renderRequest();
        this.#requestOffers();
        this.#bindEvents();


    }

    #bindEvents() {
        $("#btn-edit-request").click(() => {
            const requestModal = new RequestModal((data) => this.#onEditRequest(data));
            requestModal.show(this.request);
        });

        $(".btn-offer").click(() => {
            const offerModal = new OfferModal((data) => this.#onMakeOffer(data));
            offerModal.show(this.request);
        });
    }

    #onEditRequest(data) {
        this.request = data;
        this.#renderRequest();
    }

    #onMakeOffer(data) {
        this.request.offers.push({
            offerer: service.currentUser,
            ...data
        });
        this.#requestOffers();
    }

    #renderRequest() {
        service.fillDataValue('.request', {
            request: this.request
        });
        $(".request-status").addClass(`status-${this.request.status.toLowerCase()}`)

        $("#offering-skills").html(
            this.request.offering.skills.map(skill => $('<div></div>').addClass('skill-chip').text(skill.name))
        );
    }

    #requestOffers() {
        $("#offers").html(
            this.request.offers.map(offer => service.fillDataValue(this.templates.offer, offer))
        );
    }

    #template() {
        return $.get(`src/pages/request.page.html`);
    }
}

export const Page = RequestPage;