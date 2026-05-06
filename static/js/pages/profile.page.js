import { httpService } from '../services/http.service.js';
import { ConfirmationModal } from '../modals/confirmation.modal.js';
import { MessageModal } from '../modals/message.modal.js';
import { SkillModal } from '../modals/skill.modal.js';

class ProfilePage {
  constructor() {
    this.csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    this.initEventListeners();
  }

  initEventListeners() {
    // Open modal to add a new skill
    $('.btn-add-skill').click(() => {
      new SkillModal(null, () => {
        new MessageModal('Skill added successfully!', () => {
          location.reload();
        }).show();
      }).show();
    });

    // Open modal to edit an existing skill
    $('#offer-skills-list').on('click', '.btn-edit-skill', (e) => {
      const row = e.currentTarget.closest('.skill-row');
      const skillId = row.getAttribute('data-skill-id');
      
      new SkillModal(skillId, () => {
        new MessageModal('Skill updated successfully!', () => {
          location.reload();
        }).show();
      }).show();
    });

    // Delete a skill
    $('#offer-skills-list').on('click', '.btn-delete-skill', (e) => {
      const row = e.currentTarget.closest('.skill-row');
      const skillId = row.getAttribute('data-skill-id');
      const name = row.querySelector('.skill-name').textContent;

      new ConfirmationModal(`Are you sure you want to remove "${name}" from your profile?`, async (confirmed) => {
        if (confirmed) {
          try {
            await httpService.delete(this.csrfToken, `/api/skills/${skillId}`);
            new MessageModal(`Skill "${name}" has been removed.`, () => {
              location.reload();
            }).show();
          } catch (error) {
            console.error("Failed to delete skill", error);
            new MessageModal('Failed to delete skill. Please try again.').show();
          }
        }
      }).show();
    });
  }
}

$(document).ready(() => {
  new ProfilePage();
});