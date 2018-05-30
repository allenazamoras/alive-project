<template>
  <div>
    
  </div>
</template>

<script>
import OT from '@opentok/client';
export default {
  name: 'publisher',
  props: {
    session: {
      type: OT.Session,
      required: false
    },
  },
  mounted: function() {
    const publisher = OT.initPublisher(this.$el, {name: "You", style:{ nameDisplayMode: "on"}, fitMode: "contain", width: 150, height: 150}, (err) => {
      if (err) {
        this.$emit('error', err);
      } else {
        this.$emit('publisherCompleted');
      }
    });
    this.$emit('publisherCreated', publisher);
    const publish = () => {
      this.session.publish(publisher, (err) => {
        if (err) {
          this.$emit('error', err);
        } else {
          this.$emit('publisherConnected', publisher);
        }
      });
    };
    if (this.session && this.session.isConnected()) {
      publish();
    }
    if (this.session) {
      this.session.on('sessionConnected', publish);
    }
  }
};
</script>