# Welcome to sybil-sanctum 👋
![Version](https://img.shields.io/badge/version-1.2.1-blue.svg?cacheSeconds=2592000)

> Sybil Sanctum is an advanced tool designed to provide detailed, real-time analysis of the cryptocurrency market using the CoinGecko API and web scraping techniques. This project automates data collection and report generation through four main workflows, keeping users up-to-date with the latest trends and developments in the crypto space.

## Key Features
1. **Top 10 Coins of the Week**  
   Generates a ranking of the top 10 cryptocurrencies from the past 7 days, based on the percentage difference between their highest and lowest values.
   
2. **Chain Information**  
   Provides detailed analysis of the most relevant blockchain networks, including their activity and trends.
   
3. **Newly Listed Coins Today**  
   Tracks all cryptocurrencies that have been added to the market in the last 24 hours.
   
4. **Newly Listed Coins in the Last Hour**  
   Uses web scraping to identify and display cryptocurrencies that have just entered the market.

## Automated Notifications
The generated reports are automatically sent to a **Telegram** group using the `requests` library, enabling quick and efficient access to the information for interested users.

## Techniques and Technologies Used
- **CoinGecko API**: Integrated with the `requests` library to retrieve real-time market data.
- **Web Scraping**: Implemented with **urllib.request** to avoid bot detection and ensure successful website connections.
- **Automated Workflows**: Configured in **GitHub Actions** to ensure periodic and consistent task execution.
- **Python**: The primary language for the business logic.

## Purpose
The project aims to simplify the monitoring of new opportunities in the crypto market, delivering key insights to analysts, investors, and blockchain enthusiasts in a centralized, clear, and actionable manner.

## Inspiration
The name *Sybil Sanctum* reflects the project’s goal: to act as a "sanctuary of revelations," where crucial information about new cryptocurrencies and market trends is collected and presented in a reliable and organized way.

## Author

👤 **Beatriz Ruiz Casanova**

* Github: [@bruizk](https://github.com/bruizk)
* LinkedIn: [@beatriz-ruiz-casanova](https://www.linkedin.com/in/beatriz-ruiz-casanova/)

