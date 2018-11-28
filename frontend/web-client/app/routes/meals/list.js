import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';
import { decamelize } from '@ember/string';

export default Route.extend(AuthenticatedRouteMixin, {

  queryParams: {
    p: { refreshModel: true },
    startDatetime: { refreshModel: true },
    endDatetime: { refreshModel: true },
    startTime: { refreshModel: true },
    endTime: { refreshModel: true },
  },

  store: inject(),

  model(params) {
    let queryParams = this._buildQueryOptions(params);
    return {
      meals: this.get('store').query('meal', queryParams)
    }
  },

  _buildQueryOptions(params) {
    let queryParams = {};

    Object.keys(params).forEach(key => {
      queryParams[decamelize(key)] = params[key];
    });

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
