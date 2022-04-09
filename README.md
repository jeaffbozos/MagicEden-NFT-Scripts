# MagicEden-NFT-Scripts

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This repo contains scripts that access NFT APIs such as MagicEden (marketplace) or HowRare.is (rarity tools) to analyze the Solana NFT market. These tools are designed to add to the original features MagicEden provides. At the point of writing each script MagicEden has not implemented the feature (to the best of my knowledge). If at any point MagicEden implements a feature in this repo or a similar feature I will do my best to note it in the sections below.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **WARNING:** This repo is currently in the early stages of development. While in the early stages scripts are added when they function not when they are made most convenient to the user. The scripts below should function; however, are prone to UX/UI changes (ex: input style, number of collections, extra input flags). Expect more scripts, more configurations, and better error handling in the future.

## Contents
- [Finding Market Symbols](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Finding-Market-Symbols)
- [Scripts](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Scripts)  
  - [Deal Sniper](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Deal-Finder)  
  - [Wallet Attribute Evaluation](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Wallet-Attribute-Evaluation)  
- [Find Me](https://github.com/WilliamAmbrozic/Solana-NFT-Analytics-Tools#find-me)
- [Tip Jar](https://github.com/WilliamAmbrozic/Solana-NFT-Analytics-Tools#Solana-Tip-Jar)

## Finding Market Symbols
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Any reference to a collection symbol in this repo refers to the collection symbols assigned to collections by API providers (MagicEden, HowRare.is). 

**HowRare.is Collection Symbol:**

![HowRare](https://imgur.com/QgD1QYI.png)

* Search the collection in the search bar, the code after the ```/``` in the url is your collections HowRare.is collection symbol

**MagicEden Collection Symbol:**

![MagicEden](https://imgur.com/KF80Rwn.png)

* Search the collection in the search bar, the code after the ```/marketplace/``` in the url is your collections MagicEden collection symbol

## Scripts

## Deal Sniper

[[Back to contents]](https://github.com/WilliamAmbrozic/Solana-NFT-Analytics-Tools#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The ```deal_sniper.py``` script will output the top ```top_n``` deals found for a specified collection on MagicEden by HowRare.is rarity. All listings are looked at and placed in a hashmap that is sorted by values calculated through the following function:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Deal Ratio :=** (NFT_RANK / NFTS_IN_COLLECTION) * LISTING_PRICE

**DEMO:**

![demo](https://imgur.com/WKNhXWr.png)

**Run With:**

```python3 deal_sniper.py ME_COLLECTION_SYMBOL HR_COLLECTION_SYMBOL top_n```

For Example:

```python3 deal_sniper.py gooney_toons gooneytoons 15```

or (top 10 default):

```python3 deal_sniper.py gooney_toons gooneytoons```

## Wallet Attribute Evaluation

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MagicEden provides an evaluation of a users wallet by the floor value of each NFT. This evaluation is clearly a lower bound on the true market value of the NFTs in a wallet because it ignores attribute rarity. The ```wallet_evaluation.py``` will instead look and add up the value of each NFT by it's highest attribute floor. Attributes with no floor are given a value of zero (this will likely change). For now the script will only look at one collection at a time in a users wallet.

**Run With:**

```python3 wallet_evaluation.py WALLET_ADDR ME_COLLECTION_SYMBOL```

For Example:

```python3 wallet_evaluation.py 8vU6RfyFDk9WriVgaJohBxqtE86TLtjAR8cPWjdU6zEN gooney_toons```


## Find Me

- [williamambrozic.info](https://williamambrozic.info)
- [Twitter](https://twitter.com/WilliamAmbrozic)

## Solana Tip Jar
  * wia.sol 
  * 8vU6RfyFDk9WriVgaJohBxqtE86TLtjAR8cPWjdU6zEN
### Bitcoin
  * bc1qa7vkam2w4cgw8njqx976ga5ns8egsq3yzxzlrt



