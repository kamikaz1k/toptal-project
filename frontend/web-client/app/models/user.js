import DS from 'ember-data';
const { attr } = DS;

export default DS.Model.extend({
  email: attr('string'),
  name: attr('string'),
  caloriesPerDay: attr('number'),
  active: attr('boolean')
});
