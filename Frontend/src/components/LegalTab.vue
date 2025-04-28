<template>
  <div class="h-full flex flex-col overflow-hidden">
    <header class="border-b py-4 px-6">
      <h1 class="text-2xl font-bold">Legal</h1>
      <p class="text-muted-foreground text-sm mt-1">View Legal content</p>
    </header>

    <div class="flex flex-col md:flex-row flex-1 overflow-hidden">
      <!-- Settings Navigation -->
      <div class="w-full md:w-64 shrink-0 border-r bg-card">
        <nav class="p-2">
          <Button
            v-for="tab in tabs"
            :key="tab.id"
            :variant="currentTab === tab.id ? 'default' : 'ghost'"
            class="w-full justify-start mb-1 gap-2 font-medium"
            @click="currentTab = tab.id"
          >
            <component :is="tab.icon" class="h-4 w-4" />
            {{ tab.name }}
          </Button>
        </nav>
      </div>

      <!-- Settings Content -->

      <div class="w-full h-full p-6">
        <ScrollArea
          class="editor w-full h-full overflow-y-auto bg-primary-foreground rounded-lg border border-input"
        >
          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="currentTab === 'TermsAndConditions'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Terms and Conditions:</CardTitle>
                  <CardDescription class="text-sm text-gray-500 mb-4">
                    Last Updated: 25/4/25
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-6">
                    <!-- Profile section with improved layout -->
                    <div class="flex flex-col md:flex-row md:items-start gap-8">
                      <div class="pr-4">
                        <p class="mb-4 text-sm">
                          Welcome to NovaNote ("the App"), provided by Henry
                          Field ("Company," "we," "us," or "our"). By creating
                          an account, accessing, or using the App, you agree to
                          these Terms and Conditions ("Terms"). If you do not
                          agree, please do not use the App.
                        </p>

                        <h3 class="font-semibold mb-2">
                          0. Academic Nature of the App
                        </h3>
                        <p class="mb-2 text-sm">
                          0.1. This App is part of an academic project and is
                          provided as-is for experimental or educational use
                          only.
                        </p>
                        <p class="mb-2 text-sm">
                          0.2. We make no guarantees of availability,
                          reliability, or long-term support of either the
                          application or data stored.
                        </p>
                        <p class="mb-4 text-sm">
                          0.3. The App may be shut down or altered at any time
                          without notice.
                        </p>

                        <h3 class="font-semibold mb-2">
                          1. Account Registration and Security
                        </h3>
                        <p class="mb-2 text-sm">
                          1.1. To use the App, you must create an account and
                          provide accurate, up-to-date information.
                        </p>
                        <p class="mb-2 text-sm">
                          1.2. You are responsible for maintaining the
                          confidentiality of your password and account
                          credentials.
                        </p>
                        <p class="mb-4 text-sm">
                          1.3. All passwords are encrypted for security;
                          however, you acknowledge that no system is completely
                          secure.
                        </p>

                        <h3 class="font-semibold mb-2">
                          2. User-Generated Content
                        </h3>
                        <p class="mb-2 text-sm">
                          2.1. You retain ownership of any notes, text, images,
                          or other content ("User Content") you create within
                          the App.
                        </p>
                        <p class="mb-2 text-sm">
                          2.2. User Content is not encrypted. You acknowledge
                          and accept any risks associated with storing
                          unencrypted data.
                        </p>
                        <p class="mb-4 text-sm">
                          2.3. You grant us a non-exclusive, worldwide,
                          royalty-free license to use, store, display, and
                          distribute User Content as necessary to operate the
                          App.
                        </p>

                        <h3 class="font-semibold mb-2">
                          3. Intellectual Property
                        </h3>
                        <p class="mb-2 text-sm">
                          3.1. All software, designs, logos, trademarks, and
                          other elements of the App are owned by or licensed to
                          the Company.
                        </p>
                        <p class="mb-4 text-sm">
                          3.2. You may not copy, modify, distribute, or
                          reverse-engineer any part of the App without our
                          express permission.
                        </p>

                        <h3 class="font-semibold mb-2">
                          4. Data Privacy & Security
                        </h3>
                        <p class="mb-2 text-sm">
                          4.1. While passwords are encrypted, User Content is
                          stored in plaintext and is not encrypted. By using the
                          App, you accept this limitation.
                        </p>
                        <p class="mb-2 text-sm">
                          4.2. We take reasonable security measures to protect
                          your data but cannot guarantee complete security.
                        </p>
                        <p class="mb-4 text-sm">
                          4.3. Our use of personal data is governed by our
                          Privacy Policy.
                        </p>

                        <h3 class="font-semibold mb-2">
                          5. Prohibited Conduct
                        </h3>
                        <p class="mb-2 text-sm">5.1. You agree not to:</p>
                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Use the App for any illegal or unauthorised
                            purposes.
                          </li>
                          <li class="mb-1">
                            Upload content that infringes on third-party rights.
                          </li>
                          <li class="mb-1">
                            Attempt to hack, disrupt, or misuse the App.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">6. Termination</h3>
                        <p class="mb-2 text-sm">
                          6.1. We may suspend or terminate your account if you
                          violate these Terms.
                        </p>
                        <p class="mb-4 text-sm">
                          6.2. You may delete your account at any time, but some
                          data may be retained for legal or operational
                          purposes.
                        </p>

                        <h3 class="font-semibold mb-2">
                          7. Disclaimers & Liability Limits
                        </h3>
                        <p class="mb-2 text-sm">
                          7.1. The App is provided "as is" without warranties of
                          any kind.
                        </p>
                        <p class="mb-4 text-sm">
                          7.2. We are not responsible for any loss, damage, or
                          unauthorised access to your data.
                        </p>

                        <h3 class="font-semibold mb-2">
                          8. Changes to These Terms
                        </h3>
                        <p class="mb-4 text-sm">
                          8.1. We may update these Terms from time to time.
                          Continued use of the App after updates means you
                          accept the new Terms.
                        </p>

                        <h3 class="font-semibold mb-2">9. Contact Us</h3>
                        <p class="mb-4 text-sm">
                          If you have any questions, please contact us at
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div v-if="currentTab === 'PrivacyPolicy'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Privacy Policy:</CardTitle>
                  <CardDescription class="text-sm text-gray-500 mb-4">
                    Last Updated: 28/4/25
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-6">
                    <!-- Profile section with improved layout -->
                    <div class="flex flex-col md:flex-row md:items-start gap-8">
                      <div class="pr-4">
                        <p class="mb-4 text-sm">
                          Welcome to NovaNote (“the App”) . We respect your
                          privacy and are committed to protecting your personal
                          data. This Privacy Policy explains how we collect,
                          use, and store your information when you use the App.
                          The App is provided by Henry Field (“Company,” “we,”
                          “us,” or “our”) as part of an academic project, not
                          for commercial purposes. We comply with the UK General
                          Data Protection Regulation (“UK GDPR”) and the Data
                          Protection Act 2018.
                        </p>

                        <h3 class="font-semibold mb-2">1. Who We Are</h3>
                        <p class="mb-4 text-sm">
                          Henry Field is the data controller for the purposes of
                          UK data protection law. If you have any questions,
                          please contact us at:
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>

                        <h3 class="font-semibold mb-2">
                          2. What Data We Collect
                        </h3>
                        <p class="mb-2 text-sm">
                          When you register or use the App, we collect:
                        </p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">Your email address</li>
                          <li class="mb-1">A username of your choice</li>
                        </ul>

                        <p class="mb-4 text-sm">
                          We do not collect any sensitive personal data, such as
                          health information or financial data.
                        </p>

                        <h3 class="font-semibold mb-2">
                          3. How We Use Your Data
                        </h3>
                        <p class="mb-2 text-sm">
                          We use your information for the following purposes:
                        </p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">
                            To create and manage your account
                          </li>
                          <li class="mb-1">
                            To provide you access to the App and its features
                          </li>
                          <li class="mb-1">
                            For academic research and analysis (in anonymised or
                            aggregated form)
                          </li>
                          <li class="mb-1">
                            To communicate with you if necessary about
                            service-related issues
                          </li>
                        </ul>

                        <p class="mb-4 text-sm">
                          We do not use your data for marketing purposes or
                          targeted advertising.
                        </p>

                        <h3 class="font-semibold mb-2">
                          4. Legal Basis for Processing
                        </h3>
                        <p class="mb-2 text-sm">
                          Under the UK GDPR, our lawful basis for processing
                          your personal data is:
                        </p>
                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Consent — when you create an account, you consent to
                            us using your information as described.
                          </li>
                          <li class="mb-1">
                            Legitimate interests — to operate and improve the
                            App for academic and research purposes.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">
                          5. How We Store and Protect Your Data
                        </h3>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Your data is stored securely on hardware owned an
                            operated by the company in the UK.
                          </li>
                          <li class="mb-1">Passwords are encrypted.</li>
                          <li class="mb-1">
                            We take reasonable steps to protect your information
                            but no system is completely secure.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">6. Data Sharing</h3>
                        <p class="mb-2 text-sm">
                          We do not sell, rent, or share your personal data with
                          third parties.
                        </p>
                        <p class="mb-2 text-sm">
                          We may utilise anonymised, aggregated data for
                          academic research purposes only.
                        </p>
                        <p class="mb-4 text-sm">
                          We may disclose personal data if required to do so by
                          law.
                        </p>

                        <h3 class="font-semibold mb-2">7. Data Retention</h3>
                        <p class="mb-2 text-sm">
                          We will retain your personal information for as long
                          as necessary for the academic project.
                        </p>
                        <p class="mb-4 text-sm">
                          Once the project ends or your account is deleted, your
                          data will either be anonymised or securely deleted
                          within 30 days.
                        </p>

                        <h3 class="font-semibold mb-2">
                          8. Your Rights Under UK GDPR
                        </h3>
                        <p class="mb-2 text-sm">
                          You have the following rights:
                        </p>
                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            The right to access your personal data
                          </li>
                          <li class="mb-1">
                            Right to correct inaccurate or incomplete data
                          </li>
                          <li class="mb-1">
                            Right to request deletion of your data (“right to be
                            forgotten”)
                          </li>
                          <li class="mb-1">
                            The right to restrict processing of your data
                          </li>
                          <li class="mb-1">
                            Right to withdraw consent at any time
                          </li>
                        </ul>

                        <p class="mb-2 text-sm">
                          To exercise any of these rights, please contact us at
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>

                        <p class="mb-4 text-sm">
                          If you are unhappy with how we handle your data, you
                          can also complain to the UK Information Commissioner’s
                          Office (ICO):
                          <a
                            href="https://ico.org.uk/concerns/"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="text-primary hover:underline"
                            >https://ico.org.uk/concerns/</a
                          >
                        </p>

                        <h3 class="font-semibold mb-2">
                          9. Use of Local Storage and Session Storage
                        </h3>
                        <p class="mb-2 text-sm">
                          We use your device’s local storage and session storage
                          to enhance your experience within the App.
                          Specifically, we use storage for the following
                          purposes:
                        </p>
                        <p class="mb-2 text-sm">Session Storage:</p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">
                            We temporarily store authentication tokens during
                            your active session to enable secure login and
                            access to your account features.
                          </li>
                          <li class="mb-1">
                            To maintain your session state and preferences.
                          </li>
                        </ul>
                        <p class="mb-2 text-sm">Local Storage:</p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">
                            We store your documents locally on your device to
                            allow for offline access to your notes and content
                            when you are not connected to the internet.
                          </li>
                          <li class="mb-1">
                            We store user preferences and settings to enhance
                            your experience within the App.
                          </li>
                          <li class="mb-1">
                            We store authentication tokens to allow for
                            "remember me" functionality, enabling you to stay
                            logged in across browsing sessions.
                          </li>
                          <li class="mb-1">
                            We do not use local storage to track your activity
                            or collect personal data.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">
                          10. Changes to This Privacy Policy
                        </h3>
                        <p class="mb-4 text-sm">
                          We may update this Privacy Policy occasionally. If
                          significant changes are made, we will notify users via
                          the App or by email.
                        </p>

                        <h3 class="font-semibold mb-2">11. Contact us</h3>
                        <p class="mb-4 text-sm">
                          If you have any questions about this Privacy Policy or
                          how your data is handled, please contact:
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div v-if="currentTab === 'Acknowledgements'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Acknowledgements:</CardTitle>
                  <CardDescription class="text-sm text-gray-500 mb-4">
                    Last Updated: 28/4/25
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <!-- 
                  
                  - vue js
                  cytoscape and extensions
                  
                  shadcn
                  
                  lucide icons
                  
                  vue pinia
                  
                  Fabric js

                  
                  vue router
                  
                  axios
                  
                  tiptap
                  
                  tailwind
                  
                  postgres
                  
                  Flask
                  
                  SQL alchemy
                  
                  Py JWt-->

                  <div class="space-y-6">
                    <!-- Profile section with improved layout -->
                    <div class="flex flex-col md:flex-row md:items-start gap-8">
                      <div class="pr-4">
                        <p class="mb-4 text-sm">
                          This project uses the following open-source libraries
                          whose authors have graciously made their work
                          available for public use:
                        </p>

                        <h3 class="font-semibold mb-2">Vue.js</h3>
                        <p class="mb-2 text-sm">
                          Vue.js is a progressive JavaScript framework for
                          building user interfaces.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2018-present, Yuxi (Evan)
                            You and Vue contributors
                          </li>
                          <li class="mb-1">
                            Licence: Mit -
                            <a
                              href="https://github.com/vuejs/core/blob/main/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/vuejs/core/blob/main/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://vuejs.org/"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://vuejs.org/</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Vue Pinia</h3>
                        <p class="mb-2 text-sm">
                          Pinia is an state management library for Vue.js
                          allowing this appication to store note data and user
                          preferences webapp-wide
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2019-present Eduardo San
                            Martin Morote
                          </li>
                          <li class="mb-1">
                            Licence: Mit -
                            <a
                              href="https://github.com/vuejs/pinia/blob/v3/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/vuejs/pinia/blob/v3/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://pinia.vuejs.org"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://pinia.vuejs.org</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Vue Router</h3>
                        <p class="mb-2 text-sm">
                          Vue Router is the official router for Vue.js, enabling
                          navigation between different views and components.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2019-present Eduardo San
                            Martin Morote
                          </li>
                          <li class="mb-1">
                            Licence: Mit -
                            <a
                              href="https://github.com/vuejs/router/blob/main/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/vuejs/router/blob/main/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://router.vuejs.org"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://router.vuejs.org</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Shadcn UI</h3>
                        <p class="mb-2 text-sm">
                          Shadcn UI is a component library for Vue.js, providing
                          a set of flexible reusable UI components used system
                          wide.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2023 shadcn
                          </li>
                          <li class="mb-1">
                            Licence: Mit -
                            <a
                              href="https://github.com/shadcn-ui/ui/blob/main/LICENSE.md"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/shadcn-ui/ui/blob/main/LICENSE.md</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://ui.shadcn.com"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://ui.shadcn.com</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Tailwind CSS</h3>
                        <p class="mb-2 text-sm">
                          Tailwind CSS is a utility-first CSS framework for
                          easiily styling components and layouts.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) Tailwind Labs, Inc.
                          </li>
                          <li class="mb-1">
                            Licence: Mit -
                            <a
                              href="https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://tailwindcss.com"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://tailwindcss.com</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Lucide Icon</h3>
                        <p class="mb-2 text-sm">
                          Lucide Icon provides a set of open-source icons for
                          use in web applications.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) for portions of Lucide are
                            held by Cole Bemis 2013-2022 as part of Feather
                            (MIT). All other copyright (c) for Lucide are held
                            by Lucide Contributors 2022.
                          </li>
                          <li class="mb-1">
                            Licence: ISC -
                            <a
                              href="https://lucide.dev/license"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://lucide.dev/license</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://lucide.dev"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://lucide.dev</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Axios</h3>
                        <p class="mb-2 text-sm">
                          Axios is a promise-based HTTP client for the browser,
                          used for making API requests.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2014-present Matt Zabriskie
                            & Collaborators
                          </li>
                          <li class="mb-1">
                            Licence: MIT -
                            <a
                              href="https://github.com/axios/axios/blob/v1.x/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/axios/axios/blob/v1.x/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://axios-http.com/docs/intro"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://axios-http.com/docs/intro</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Cytoscape JS</h3>
                        <p class="mb-2 text-sm">
                          Cytoscape.js is a graph theory library for
                          visualisation and analysis of graphs and networks.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2016-2024, The Cytoscape
                            Consortium.
                          </li>
                          <li class="mb-1">
                            Licence: MIT -
                            <a
                              href="https://github.com/cytoscape/cytoscape.js/blob/unstable/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/cytoscape/cytoscape.js/blob/unstable/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://js.cytoscape.org"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://js.cytoscape.org</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">TipTap</h3>
                        <p class="mb-2 text-sm">
                          TipTap is a rich-text editor framework for Vue.js,
                          providing a flexible and extensible way to create text
                          editing experiences.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2025, Tiptap GmbH
                          </li>
                          <li class="mb-1">
                            Licence: MIT -
                            <a
                              href="https://github.com/ueberdosis/tiptap/blob/develop/LICENSE.md"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/ueberdosis/tiptap/blob/develop/LICENSE.md</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://tiptap.dev"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://tiptap.dev</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Fabric Js</h3>
                        <p class="mb-2 text-sm">
                          Fabric.js is a powerful and simple JavaScript HTML5
                          canvas library, providing an interactive object model
                          on top of the canvas element.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2008-2015 Printio (Juriy
                            Zaytsev, Maxim Chernyak)
                          </li>
                          <li class="mb-1">
                            Licence: MIT -
                            <a
                              href="https://github.com/fabricjs/fabric.js/blob/master/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/fabricjs/fabric.js/blob/master/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://fabricjs.com"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://fabricjs.com</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">Python Flask</h3>
                        <p class="mb-2 text-sm">
                          Flask is a lightweight WSGI web application framework
                          in Python, used for building web applications and
                          APIs.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright 2010 Pallets
                          </li>
                          <li class="mb-1">
                            Licence: BSD-3 -
                            <a
                              href="https://github.com/pallets/flask/blob/main/LICENSE.txt"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/pallets/flask/blob/main/LICENSE.txt</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://flask.palletsprojects.com/en/stable/"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://flask.palletsprojects.com/en/stable/</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">SQL Alchemy</h3>
                        <p class="mb-2 text-sm">
                          SQLAlchemy is a SQL toolkit and Object-Relational
                          Mapping (ORM) system for Python, providing a full
                          power and flexibility of SQL.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright 2005-2025 SQLAlchemy authors
                            and contributors
                          </li>
                          <li class="mb-1">
                            Licence: MIT -
                            <a
                              href="https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://www.sqlalchemy.org"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://www.sqlalchemy.org</a
                            >
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">PY JWt</h3>
                        <p class="mb-2 text-sm">
                          PyJWT is a Python library for encoding and decoding
                          JSON Web Tokens (JWT), used for secure data exchange
                          between parties.
                        </p>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Copyright: Copyright (c) 2015-2022 José Padilla
                          </li>
                          <li class="mb-1">
                            Licence: MIT -
                            <a
                              href="https://github.com/jpadilla/pyjwt/blob/master/LICENSE"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://github.com/jpadilla/pyjwt/blob/master/LICENSE</a
                            >
                          </li>
                          <li class="mb-1">
                            Reference:
                            <a
                              href="https://pyjwt.readthedocs.io/en/stable/"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline"
                              >https://pyjwt.readthedocs.io/en/stable/</a
                            >
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </ScrollArea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import axios, { getBaseUrl } from "../axios.js";
import { useToast } from "@/components/ui/toast/use-toast";
import { useGraphStore } from "@/stores/useGraphStore";
import { useUserStore } from "@/stores/useUserStore";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import {
  User,
  Palette,
  Puzzle,
  Settings as SettingsIcon,
  Check,
  Sun,
  Moon,
  Monitor,
  FileText,
  Eye,
  Brain,
  Calculator,
  Calendar,
  Clock,
  Code,
  EyeOff,
  Handshake,
} from "lucide-vue-next";

const graphStore = useGraphStore();
const userStore = useUserStore();
const { toast } = useToast();

// Tab navigation
const currentTab = ref("TermsAndConditions");
const tabs = [
  { id: "TermsAndConditions", name: "Terms And Conditions", icon: Handshake },
  { id: "PrivacyPolicy", name: "Privacy Policy", icon: EyeOff },
  { id: "Acknowledgements", name: "Acknowledgements", icon: Puzzle },
];

// Load user data on component mount
onMounted(() => {});
</script>
