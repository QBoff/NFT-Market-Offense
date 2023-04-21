// https://eth-sepolia.g.alchemy.com/v2/MoYuuv1ZLGEYBscg47QOit9y3cp_S2YO

require('@nomiclabs/hardhat-waffle');

module.exports = {
  solidity: '0.8.9',
  networks: {
    sepolia: {
      url: 'https://eth-sepolia.g.alchemy.com/v2/MoYuuv1ZLGEYBscg47QOit9y3cp_S2YO',
      accounts: [ '42f10121e5e8e31e1a272fb4839cb9425f3c07874783ccc8ab0b1905efe845c8' ]
    }
  }
}