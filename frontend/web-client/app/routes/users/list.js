import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  store: inject(),

  model(params) {
    return {
      users: this.get('store').query('user', { p: 1 })
    }
  },

  actions: {
    deleteUser(userId) {
      console.log("delete!", userId);
      let user = this.get('store').peekRecord('user', userId);
      if (user) {
        user.deleteRecord();
        user.save().then(() => {
          console.log("deleted userId ", userId);
        }).catch(e => {
          console.error(e);
          alert("something went wrong...");
        })
      }
    }
  }

});
