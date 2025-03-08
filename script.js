let currentStep = 0;
const formSteps = document.querySelectorAll('.form-step');

document.addEventListener('DOMContentLoaded', () => {
    showStep(currentStep);
});

function showStep(step) {
    formSteps.forEach((formStep, index) => {
        formStep.classList.toggle('active', index === step);
    });
}

function nextStep() {
    if (currentStep < formSteps.length - 1) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        showStep(currentStep);
    }
}

// Function to handle the form submission
async function generateMealPlan() {
    document.getElementById('nutritionForm').style.display = 'none';
    document.getElementById('mealPlanButton').style.display = 'block';
}

// Function to fetch and display the meal plan
async function showMealPlan() {
    const formData = new FormData(document.getElementById('nutritionForm'));
    const userData = {};

    formData.forEach((value, key) => {
        userData[key] = value;
    });

    console.log("Sending data:", userData);

    try {
        const response = await fetch('http://127.0.0.1:5000/generate_meal_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();
        console.log("Meal plan response:", result);

        if (result.meal_plan) {
            displayMealPlan(result.meal_plan);
        } else {
            alert("Error generating meal plan. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server.");
    }
}

// Function to display the meal plan in the HTML page
function displayMealPlan(mealPlan) {
    let outputDiv = document.getElementById("mealPlanOutput");

    if (!outputDiv) {
        console.error("mealPlanOutput div not found!");
        return;
    }

    // Insert the meal plan directly as HTML
    outputDiv.innerHTML = mealPlan;

    // Make sure the meal plan container is visible
    document.getElementById('mealPlanContainer').style.display = 'block';
    document.getElementById('backToFormButton').style.display = 'block';
}

// Function to go back to the form
function goBackToForm() {
    document.getElementById('mealPlanContainer').style.display = 'none';
    document.getElementById('mealPlanButton').style.display = 'none';
    document.getElementById('nutritionForm').style.display = 'block';

    currentStep = 0;
    showStep(currentStep);
}

// New function added
async function fetchData() {
    let data = await someAsyncFunction();
    document.getElementById("output").innerText = data;
}
