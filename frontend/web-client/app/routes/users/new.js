import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  model() {
    return this.get('store').createRecord('user')
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
