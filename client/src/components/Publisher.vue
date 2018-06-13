<template>
  <div>
    
  </div>
</template>

<script>
import OT from '@opentok/client'
import {mapState} from 'vuex'

export default {
  name: 'publisher',
  props: {
    session: {
      type: OT.Session,
      required: false
    },
  },

  computed: { 
    ...mapState('userModule', [
      'username'
    ])
  },

  mounted: function() {
    const publisher = OT.initPublisher(this.$el, {name: this.username, style:{ nameDisplayMode: "on"}, fitMode: "contain", width: 128, height: 72}, (err) => {
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