import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  store: inject(),

  model() {
    return {
      meals: this.get('store').query('meal', { p: 1 })
    }
  },

  actions: {
    deleteMeal(mealId) {
      console.log("delete!", mealId);
      let meal = this.get('store').peekRecord('meal', mealId);
      if (meal) {
        meal.deleteRecord();
        meal.save().then(() => {
          console.log("deleted mealId ", mealId);
        }).catch(e => {
          console.error(e);
          alert("something went wrong...");
        })
      }
    }
  }

});
