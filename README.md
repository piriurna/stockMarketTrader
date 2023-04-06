# Stock Market Analysis

This project provides a Python-based tool for fetching, analyzing, and visualizing stock market data. It uses the Alpha Vantage API for retrieving stock prices and calculates simple moving averages (SMA) to help you identify trends and make informed trading decisions. The project is structured to be modular, maintainable, and easily expandable.

## Features

-   Fetch stock data from the Alpha Vantage API
-   Process and store stock data in pandas DataFrames
-   Calculate simple moving averages (SMA) for various window lengths
-   Visualize stock prices and moving averages using matplotlib
-   Modular and easily expandable code structure

## Dependencies

-   Python 3.6+
-   pandas
-   matplotlib
-   requests

## Installation

1.  Clone the repository:
    
    bashCopy code
    
    `git clone https://github.com/yourusername/stock_analysis.git` 
    
2.  Navigate to the project directory:
    
    bashCopy code
    
    `cd stock_analysis` 
    
3.  Install the required dependencies using pip:
    
    Copy code
    
    `pip install -r requirements.txt` 
    

## Usage

1.  Sign up for a free Alpha Vantage API key [here](https://www.alphavantage.co/support/#api-key).
    
2.  Open `src/main.py` and replace `'your_alpha_vantage_api_key'` with your actual API key.
    
3.  Choose the stock symbol you want to analyze by modifying the `symbol` variable in `src/main.py`.
    
4.  Run the `main.py` script:
    
    cssCopy code
    
    `python src/main.py` 
    
5.  The script will fetch the stock data, process it, calculate the moving averages, and visualize the results in a plot.
    

## Contributing

Contributions to this project are welcome! If you'd like to improve the code, add new features, or fix bugs, feel free to fork the repository and submit a pull request. Please make sure to follow the existing code style and add appropriate tests and documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](https://chat.openai.com/chat/LICENSE) file for details.