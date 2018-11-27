import Controller from '@ember/controller';
import { computed, get } from '@ember/object';
import { inject } from '@ember/service';
import jwtDecode from 'ember-jwt-decode';

export default Controller.extend({

  session: inject(),

  isAdmin: computed('session', function() {
    let token = this.get('session.data.authenticated.token');
    if (token) {
      let decoded = jwtDecode(token);
      return !!get(decoded, 'roles.is_admin');
    }
    return false;
  }),

  isUserManager: computed('session', function() {
    let token = this.get('session.data.authenticated.token');
    if (token) {
      let decoded = jwtDecode(token);
      return !!get(decoded, 'roles.is_user_manager');
    }
    return false;
  })

});
