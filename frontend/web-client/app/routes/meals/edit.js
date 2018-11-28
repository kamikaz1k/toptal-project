import moment from 'moment';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import { inject } from '@ember/service';
import jwtDecode from 'ember-jwt-decode';

const TIME_FORMAT_AM = 'hh:mm A';
const DATE_FORMAT = 'YYYY-MM-DD';
const DATETIME_FORMAT = `${DATE_FORMAT} ${TIME_FORMAT_AM}`;

export default Route.extend(AuthenticatedRouteMixin, {

  session: inject(),

  store: inject(),

  model(params) {
    return this.get('store').findRecord('meal', params.mealId)
  },

  _buildDatetimeQuery(datetime) {
    let start_datetime = moment(datetime).startOf('day').utc();
    let end_datetime = moment(datetime).endOf('day').utc();

    return {
      start_datetime: start_datetime.toISOString(),
      end_datetime: end_datetime.toISOString()
    }
  },

  setupController(controller, model) {
    this._super(controller, model);
    let token = this.get('session.data.authenticated.token');
    let { user_id } = jwtDecode(token);

    let query = this._buildDatetimeQuery(model.get('entryDatetime'));
    this.get('store').query('meal', query).then(results => {
      controller.set('mealsOfDay', results);
    });

    this.get('store').queryRecord('user', user_id).then(result => {
      controller.set('user', result);
    });

  },

  afterModel(model) {
    let entryDatetime = model.get('entryDatetime');
    model.set(
      'userInputtedDatetime',
      moment(entryDatetime).format(DATETIME_FORMAT)
    );
  },

  actions: {
    saveMeal(model){
      model.set(
        'entryDatetime',
        moment(model.get('userInputtedDatetime'), DATETIME_FORMAT).toDate()
      )
      console.log(model);
      model.save().then(() => {
        this.transitionTo('meals.list')
      }).catch(e => {
        console.error(e);
        alert("something went wrong...")
      });
    }
  }
});
