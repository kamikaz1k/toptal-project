import DS from 'ember-data';
const { attr } = DS;

export default DS.Model.extend({
  ownerUserId: attr('number'),
  text: attr('string'),
  entryDatetime: attr('date'),
  calories: attr('number')
});
