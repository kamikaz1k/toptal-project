import moment from 'moment';
import EmberObject from '@ember/object';
import Route from '@ember/routing/route';

export default Route.extend({

  model() {
    return EmberObject.create({
      startDate: moment().format('MM-DD-YYYY'),
      endDate: moment().format('MM-DD-YYYY'),
      startTime: moment().format('hh:mm A'),
      endTime: moment().format('hh:mm A')
    });
  },

  actions: {
    setSearchParams(model) {
      let props = {
        startDate: moment(model.get('startDate'), 'MM-DD-YYYY'),
        endDate: moment(model.get('endDate'), 'MM-DD-YYYY'),
        startTime: moment(model.get('startTime'), 'hh:mm A'),
        endTime: moment(model.get('endTime'), 'hh:mm A')
      }
      console.log(model, props);
    }
  }

});
