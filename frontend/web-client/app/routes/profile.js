import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import jwtDecode from 'ember-jwt-decode';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  session: inject(),

  store: inject(),

  model() {
    let token = this.get('session.data.authenticated.token');
    let { user_id } = jwtDecode(token);

    return this.get('store').findRecord('user', user_id);
  },

  actions: {
    saveUser(model) {
      model.save().then(() => {
        this.transitionTo('meals.list');
      }).catch(e => {
        console.error(e);
        alert("something went wrong...");
      });
    }
  }

});
