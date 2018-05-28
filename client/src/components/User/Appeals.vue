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
                            <v-card dark hover @click="info(appeal)">
                                <v-card-title primary-title>
                                <div>
                                    <h3 class="body-2 mb-0"> {{ appeal.request_title }} </h3>
                                    <div class="caption"> {{ appeal.detail }} </div>
                                </div>
                                </v-card-title>
                            </v-card>
                        </v-flex>
                        <v-flex v-if="closedAppeals.length == 0" xs12 class="grey--text">
                            There's nothing here.
                        </v-flex>
                    </v-layout>
                    
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
export default {
    props: ["openAppeals", "closedAppeals"]
}
</script>
