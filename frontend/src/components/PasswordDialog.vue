<template>
  <div>
    <!-- Reset Password Dialog -->
    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="headline">Forgot Password</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Email"
                  v-model="email"
                  prepend-icon="mdi-email"
                  type="email"
                  placeholder="Enter your email"
                  :rules="emailRules"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="resetPassword"
            >Reset Password</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Token Input Dialog -->
    <v-dialog v-model="tokenDialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="headline">Reset Token</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Reset Token"
                  v-model="resetToken"
                  prepend-icon="mdi-key"
                  placeholder="Enter the reset token"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="cancelToken">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="submitToken">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- New Password Dialog -->
    <v-dialog v-model="newPasswordDialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="headline">New Password</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="New Password"
                  v-model="newPassword"
                  prepend-icon="mdi-lock"
                  type="password"
                  placeholder="Enter your new password"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="cancelNewPassword"
            >Cancel</v-btn
          >
          <v-btn color="blue darken-1" text @click="confirmNewPassword"
            >Confirm</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { apiClient, toast } from "@/apiConfig";

export default {
  data() {
    return {
      dialog: false,
      tokenDialog: false,
      newPasswordDialog: false,
      email: "",
      resetToken: "",
      newPassword: "",
      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /.+@.+\..+/.test(v) || "Please enter a valid email",
      ],
    };
  },
  methods: {
    open() {
      this.dialog = true;
    },
    close() {
      this.email = "";
      this.dialog = false;
    },
    async resetPassword() {
      try {
        const response = await apiClient.post("/auth/reset-password", {
          email: this.email,
        });

        if (response.status === 200) {
          toast.success(
            response.data.message ||
              "Password reset instructions sent to your email",
          );
          this.dialog = false; // Close the reset password dialog
          this.tokenDialog = true; // Open the token input dialog
        } else {
          throw new Error("Failed to reset password. Please try again.");
        }
      } catch (error) {
        console.error("Error resetting password:", error);
        toast.error("Failed to reset password. Please try again.");
      }
    },
    cancelToken() {
      this.resetToken = ""; // Clear the token input
      this.tokenDialog = false; // Close the token input dialog
    },
    async submitToken() {
      try {
        const response = await apiClient.post("/auth/validate-token", {
          email: this.email,
          resetToken: this.resetToken,
        });

        if (response.status === 200 && response.data.isValid) {
          // Token is valid, proceed with password reset
          this.tokenDialog = false; // Close the token input dialog
          this.newPasswordDialog = true; // Open the new password input dialog
        } else {
          // Token is invalid
          toast.error("Invalid token. Please try again.");
        }
      } catch (error) {
        console.error("Error validating token:", error);
        toast.error("Failed to validate token. Please try again.");
      }
    },
    cancelNewPassword() {
      this.newPassword = ""; // Clear the new password input
      this.newPasswordDialog = false; // Close the new password input dialog
    },
    async confirmNewPassword() {
      try {
        const resetResponse = await apiClient.post(
          "/auth/reset-password-confirm",
          {
            email: this.email,
            newPassword: this.newPassword,
          },
        );

        if (resetResponse.status === 200) {
          toast.success("Password reset successful.");
          this.newPasswordDialog = false; // Close the new password input dialog
        } else {
          throw new Error("Failed to reset password. Please try again.");
        }
      } catch (error) {
        console.error("Error resetting password:", error);
        toast.error("Failed to reset password. Please try again.");
      }
    },
  },
};
</script>
