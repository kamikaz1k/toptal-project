import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  store: inject(),

  model(params) {
    return {
      users: this.get('store').query('user', { p: 1 })
    }
  }

});
