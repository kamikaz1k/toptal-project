import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  model(params) {
    return this.get('store').findRecord('user', params.userId);
  },

  actions: {
    saveUser(model){
      model.save().then(() => {
        this.transitionTo('users.list');
      }).catch(e => {
        console.error(e);
        alert("something went wrong...");
      });
    }
  }

});
