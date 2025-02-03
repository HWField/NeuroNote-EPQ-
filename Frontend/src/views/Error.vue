<script setup lang="ts">
defineProps<{
    message: string
}>()
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import LightDark from '@/components/LightDark.vue'
</script>

<template>

<div class="absolute top-4 right-4">
    <LightDark class="bg-white p-4 rounded-lg shadow-lg"></LightDark>
  </div>

<div class="flex justify-center items-center min-h-screen">
    <Card class="w-96">
        <CardHeader>
            <CardTitle>Error</CardTitle>
        </CardHeader>
        <CardContent>
        <p>{{ message }}</p>
        </CardContent>
        <CardFooter>
         Return to
         <RouterLink to="/"> Home</RouterLink>
        </CardFooter>
    </Card>
</div>
</template>