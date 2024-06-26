function calculate() {
    // Get user input values
    const investment = parseFloat(document.getElementById("investment").value);
    const rate = parseFloat(document.getElementById("rate").value) / 100;  // Convert rate to decimal
    const time = parseInt(document.getElementById("time").value);

    // Validate input (optional)
    if (isNaN(investment) || isNaN(rate) || isNaN(time) || investment <= 0 || rate <= 0 || time <= 0) {
        alert("Please enter valid positive numbers for Investment, Rate, and Time Period.");
        return;
    }

    // Calculate maturity amount
    const interestRatePerMonth = rate / 12;
    const totalNumberOfMonths = time;
    let maturityAmount = 0;

    for (let i = 0; i < totalNumberOfMonths; i++) {
        maturityAmount += investment + (maturityAmount * interestRatePerMonth);
    }

    // Display the result
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `Your maturity amount after ${time} months will be approximately ₹${maturityAmount.toFixed(2)}`;
}
