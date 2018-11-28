import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';

export default Route.extend(AuthenticatedRouteMixin, {

  store: inject(),

  queryParams: {
    p: { refreshModel: true }
  },

  model(params) {
    return {
      users: this.get('store').query('user', { p: params.p || 1 })
    }
  },

  setupController(controller, model) {
    this._super(...arguments);

    let page = parseInt(controller.get('p')) || 1;

    if (page > 1) {
      controller.set('previousPage', page - 1);
    }
    controller.set('nextPage', page + 1);

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
