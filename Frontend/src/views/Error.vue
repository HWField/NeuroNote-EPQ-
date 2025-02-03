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
</script>

<template>
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