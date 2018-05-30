<template>
  <div></div>
</template>

<script>
export default {
  name: 'subscriber',
  props: {
    stream: {
      type: OT.Stream,
      required: true
    },
    session: {
      type: OT.Session,
      required: true
    },
  },
  mounted: function() {
    const subscriber = this.session.subscribe(this.stream, this.$el, {name: "The other dude", fitMode: "contain", style: { nameDisplayMode: "on" }, width: '100%', height: 480}, (err) => {
      if (err) {
        this.$emit('error', err);
      } else {
        this.$emit('subscriberConnected', subscriber);
      }
    });
    this.$emit('subscriberCreated', subscriber);
  }
};
</script>