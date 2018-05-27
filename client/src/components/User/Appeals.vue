<template>
    <div>
        <v-container>
            <v-layout row wrap justify-center grid-list-lg pl-2 pr-2 pb-2>
                <v-flex xs12>                     
                    <v-subheader class="pl-0">
                            Active
                    </v-subheader>

                    <v-layout row wrap>
                        <v-flex xs12 v-for="(appeal, index) in appeals" :key="`appeal-${index}`" pt-0 v-if="appeal.status == 'active'">
                            <v-card color="teal" dark class="elevation-2 pb-3">
                                <!-- <v-card-media src="/static/doc-images/cards/desert.jpg" height="200px">
                                </v-card-media> -->
                                <v-card-title primary-title>
                                <div>
                                    <h2 class="headline"> {{ appeal.title }} </h2>
                                    <div> {{ appeal.detail }} </div>
                                </div>
                                </v-card-title>
                                <v-card-actions>
                                <v-btn flat class="ml-2"><v-icon>video_call</v-icon> Call</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-flex>
                    </v-layout>
                    
                </v-flex>

                <v-flex xs12>                     
                    <v-subheader class="pl-0">
                            Completed
                    </v-subheader>
                    <v-layout row wrap>
                        <v-flex xs12 v-for="(appeal, index) in appeals" :key="`appeal-${index}`" pt-0 v-if="appeal.status == 'completed'">
                            <v-card color="blue-grey darken-1" dark class="elevation-2">
                                <!-- <v-card-media src="/static/doc-images/cards/desert.jpg" height="200px">
                                </v-card-media> -->
                                <v-card-title primary-title>
                                <div>
                                    <h3 class="body-1 mb-0"> {{ appeal.title }} </h3>
                                    <div class="caption"> {{ appeal.detail }} </div>
                                </div>
                                </v-card-title>
                            </v-card>
                        </v-flex>
                    </v-layout>
                    
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
export default {
    props: ["appeals"]
}
</script>
