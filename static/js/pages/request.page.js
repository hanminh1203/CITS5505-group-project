import { RequestModal } from "../modals/request.modal.js";
import { OfferModal } from "../modals/offer.modal.js";
import { ConfirmationModal } from "../modals/confirmation.modal.js";
import { httpService } from "../services/http.service.js";
import { MessageModal } from "../modals/message.modal.js";
class RequestPage {
    requestId = null;
    constructor() {
        const dataElem = $("#request-data");
        this.csrfToken = $('meta[name="csrf-token"]').attr('content');
        this.requestId = dataElem.attr('data-request-id');
    }
    onInit() {
        $("#btn-edit-request").click(() => {
            const requestModal = new RequestModal(this.requestId, (data) => {
                location.reload();
            });
            requestModal.show();
        });
        $(".btn-offer").click(() => {
            const offerModal = new OfferModal((data) => this.onMakeOffer(data));
            offerModal.show(this.request);
        });

        $("#btn-complete-request").click(async () => {
            new ConfirmationModal("Are you sure you want to mark this request as complete? This action cannot be undone.", async (confirmed) => {
                if (confirmed) {
                    const response = await httpService.post(this.csrfToken, `/api/requests/${this.requestId}/complete`);
                    new MessageModal("Request marked as complete.", () => {
                        location.reload();
                    }).show();
                }
            }).show();
        });

        $("#btn-cancel-request").click(async () => {
            new ConfirmationModal("Are you sure you want to cancel this request? This action cannot be undone.", async (confirmed) => {
                if (confirmed) {
                    const response = await httpService.post(this.csrfToken, `/api/requests/${this.requestId}/cancel`);
                    new MessageModal("Request marked as cancelled.", () => {
                        location.reload();
                    }).show();
                }
            }).show();
        });
        
        $(".btn-cancel-offer").click(async (e) => {
            const offerId = $(e.currentTarget).data('offer-id');

            new ConfirmationModal("Are you sure you want to cancel this offer? This action cannot be undone.", async (confirmed) => {
                if (confirmed) {
                    const response = await httpService.delete(this.csrfToken, `/api/requests/${this.requestId}/offers/${offerId}`);
                    new MessageModal("Offer cancelled.", () => {
                        location.reload();
                    }).show();
                }
            }).show();
        });
    }

    onMakeOffer(data) {
        location.reload();
    }
}

export const Page = RequestPage;

$(document).ready(() => {
    new Page().onInit();
});