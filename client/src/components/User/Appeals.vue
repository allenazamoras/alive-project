<template>
    <div>
        <v-container>
            <v-layout row wrap justify-center grid-list-lg pl-2 pr-2 pb-2>
                <v-flex xs12>                     
                    <v-subheader class="pl-0">
                            Active
                    </v-subheader>

                    <v-layout row wrap>
                        <v-flex xs12 v-for="appeal in openAppeals" :key="appeal.id" pt-0 v-if="openAppeals.length > 0">
                            <v-card dark class="elevation-2 pb-3">
                                <v-card-title primary-title>
                                <div>
                                    <h2 class="headline"> {{ appeal.request_title }} </h2>
                                    <div> {{ appeal.detail }} </div>
                                </div>
                                </v-card-title>
                                <v-card-actions>
                                <v-btn flat class="ml-2"><v-icon>video_call</v-icon> Call</v-btn>
                                <v-btn flat @click="edit(appeal)" class="ml-2">Edit</v-btn>
                                <v-btn flat @click="cancel(appeal)" class="ml-2">Cancel</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-flex>
                        <v-flex v-if="openAppeals.length == 0" xs12 class="grey--text">
                            There's nothing here.
                        </v-flex>
                    </v-layout>
                    
                </v-flex>

                <v-flex xs12>                     
                    <v-subheader class="pl-0">
                            Completed
                    </v-subheader>
                    <v-layout row wrap>
                        <v-flex xs4 v-for="appeal in closedAppeals" :key="appeal.id" v-if="closedAppeals.length > 0" pt-0>
                            <v-card dark class="elevation-2">
                                <v-card-title primary-title>
                                <div>
                                    <h3 class="body-2 mb-0"> {{ appeal.request_title }} </h3>
                                    <div class="caption"> {{ appeal.detail }} </div>
                                </div>
                                </v-card-title>

                                <v-card-actions>
                                    <v-btn flat @click="edit(appeal)">
                                        edit
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-flex>
                        <v-flex v-if="closedAppeals.length == 0" xs12 class="grey--text">
                            There's nothing here.
                        </v-flex>
                    </v-layout>
                </v-flex>
            </v-layout>
            
    <snackbar :snackbar="snackbar"/>

    <v-dialog v-model="dialog" max-width="290">
      <v-card>
            <v-card-text>
                <v-form>
                    <v-text-field
                    v-model="appeal.request_title"
                    label="Title"
                    ></v-text-field>
                    <v-text-field
                    v-model="appeal.detail"
                    label="Description"
                    ></v-text-field>
                </v-form>
            </v-card-text>
            

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="save">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
        </v-container>
    </div>
</template>

<script>
import dialogThing from '../.././components/Dialog.vue'
import snackbar from '../.././components/Snackbar.vue'

import axios from 'axios'

export default {
    data() { 
        return { 
            appeal: [],
            snackbar: {},
            dialog: false,
        }
    },

    methods: { 
        edit(appeal) { 
            this.appeal = appeal
            this.dialog = true
        },

        save() { 
            axios.patch(`${process.env.API_URL}/request/${this.appeal.id}/`, {
                "request_title": this.appeal.request_title,
                "detail": this.appeal.detail
            }, this.$store.getters.getConfig)

            .then((res) => { 
                this.dialog = false

                this.snackbar = {
                    text: "Successfully updated",
                    flag: true
                }
            })

            .catch((res) => { 
                this.snackbar = {
                    text: "Unable to update appeal",
                    flag: true
                }
            })
        },

        cancel(appeal) { 
            axios.patch(`${process.env.API_URL}/request/${appeal.id}/`, {
                "status": "COMPLETED"
            }, this.$store.getters.getConfig)

            .then((res) => { 
                this.dialog = false

                this.snackbar = {
                    text: "Successfully updated",
                    flag: true
                }
            })

            .catch((res) => { 
                this.snackbar = {
                    text: "Unable to update appeal",
                    flag: true
                }
            })
        }
    },

    props: ["openAppeals", "closedAppeals"],

    components: { 
        dialogThing,
        snackbar
    }
}
</script>
