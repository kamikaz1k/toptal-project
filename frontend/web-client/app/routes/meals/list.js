import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  queryParams: {
    p: { refreshModel: true },
    startDate: {},
    endDate: {},
    startTime: {},
    endTime: {},
  },

  store: inject(),

  model(params) {
    let queryParams = this._buildQueryOptions(params);
    return {
      meals: this.get('store').query('meal', queryParams)
    }
  },

  _buildQueryOptions(params) {
    let queryParams = Object.assign({}, params);
    if (queryParams.p == undefined) {
      queryParams.p = 1;
    }
    return queryParams;
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
