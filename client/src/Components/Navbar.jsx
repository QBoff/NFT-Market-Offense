import logo from '../images/logo.png';


export const Navbar = () => {
    return <nav>
        <a href='#'> <img src={logo} alt="Logo Image" /> </a>
        <ul>
            <li> <a href="/market">Market </a> </li>
            <li> <a href="/create_nft"> Create NFT </a> </li>
            <li> <a href="/transactions"> Transactions </a> </li>
        </ul>
    </nav>;
}