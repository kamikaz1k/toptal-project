import moment from 'moment';
import EmberObject from '@ember/object';
import Route from '@ember/routing/route';

const TIME_FORMAT_AM = 'hh:mm A';
const TIME_FORMAT_ISO = 'HH:mm';
const DATE_FORMAT = 'YYYY-MM-DD';

export default Route.extend({

  model() {
    return EmberObject.create({
      startDate: null,
      endDate: null,
      startTime: moment().format(TIME_FORMAT_AM),
      endTime: moment().format(TIME_FORMAT_AM)
    });
  },

  actions: {
    setSearchParams(model) {
      let props = {
        startDate: moment(model.get('startDate'), DATE_FORMAT).format(DATE_FORMAT),
        endDate: moment(model.get('endDate'), DATE_FORMAT).format(DATE_FORMAT),
        startTime: moment(model.get('startTime'), TIME_FORMAT_AM).format(TIME_FORMAT_ISO),
        endTime: moment(model.get('endTime'), TIME_FORMAT_AM).format(TIME_FORMAT_ISO),
      }
      Object.keys(props).forEach(key => {
        if (props[key] == "Invalid date") {
          delete props[key];
        }
      });
      console.log(model, props);
      this.transitionTo('meals.list', { queryParams: props })
    }
  }

});
