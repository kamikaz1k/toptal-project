import moment from 'moment';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  store: inject(),

  model(params) {
    return this.get('store').findRecord('meal', params.mealId);
  },

  afterModel(model) {
    model.set(
      'userInputtedDatetime',
      moment(model.get('entryDatetime')).format('YYYY-MM-DD hh:mm A')
    )
  },

  actions: {
    saveMeal(model){
      model.set(
        'entryDatetime',
        moment(model.get('userInputtedDatetime'), 'YYYY-MM-DD hh:mm A').toDate()
      )
      console.log(model);
      model.save().then(() => {
        this.transitionTo('meals.list')
      }).catch(e => {
        console.error(e);
        alert("something went wrong...")
      });
    }
  }
});
