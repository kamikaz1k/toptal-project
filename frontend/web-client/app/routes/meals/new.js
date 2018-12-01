import moment from 'moment';
import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  actions: {
    saveMeal(form) {
      console.log("saveMeal", form);
      this.get('store').createRecord('meal', {
        text: form.get('text'),
        calories: form.get('calories'),
        entryDatetime: moment(form.get('entryDatetime'), 'YYYY-MM-DD hh:mm A').toDate()
      }).save().then(() => {
        this.transitionTo('meals.list');
      }).catch(e => {
        console.error(e);
        alert("Something went wrong...");
      });
    }
  }
});
