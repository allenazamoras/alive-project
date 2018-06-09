<template>
  <div>
    <app-nav />
    <v-container 
      fill-height 
      grid-list-lg
    >
      <v-layout
        row
        wrap
        justify-center
      >
        <v-flex md8>
          <div id="session">
            <publisher v-if="session" :session="session" ></publisher>
            <div id="subscribers" v-if="session" v-for="stream in streams" :key="stream.streamId">
              <subscriber :stream="stream" :session="session"></subscriber>
            </div>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Publisher from '../components/Publisher'
import Subscriber from '../components/Subscriber'
import appNav from '../components/AppNav'

import OT from '@opentok/client'

export default {
  data() { 
    return { 
      key: "46127952",
      session_id: "2_MX40NjEyNzk1Mn5-MTUyODQ2NDIwNzA3MX42ZFlpdHpEWU11c3oxUmIyb2JZTFgvOG9-fg",
      token_id: "T1==cGFydG5lcl9pZD00NjEyNzk1MiZzaWc9YjY1OTAyYzAxYzk1ZTVlODljZTVjYzQ1YmZmZGY2M2JlMjgwZGQ4MjpzZXNzaW9uX2lkPTJfTVg0ME5qRXlOemsxTW41LU1UVXlPRFEyTkRJd056QTNNWDQyWkZscGRIcEVXVTExYzNveFVtSXliMkpaVEZndk9HOS1mZyZjcmVhdGVfdGltZT0xNTI4NDY0MjMwJm5vbmNlPTAuMjA5MjI4OTA3NzkzNDEzOTcmcm9sZT1wdWJsaXNoZXImZXhwaXJlX3RpbWU9MTUzMTA1NjIyOSZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ==",

      session: null,
      streams: [],
      publisher: null,
    }
  },

  components: {
    Publisher, 
    Subscriber,
    appNav
  },

  created () {
    this.session = OT.initSession(this.key, this.session_id);
    this.session.connect(this.token_id, (err) => {
      if (err) {
        errorHandler(err);
      }
    });
    this.session.on('streamCreated', (event) => {
      this.streams.push(event.stream);
    });
    this.session.on('streamDestroyed', (event) => {
      const idx = this.streams.indexOf(event.stream);
      if (idx > -1) {
        this.streams.splice(idx, 1);
      }
    });
  }
}
</script>