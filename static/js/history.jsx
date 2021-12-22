const History = () => {
    const [history, updateHistory] = React.useState([]);
    React.useEffect(() => {
        fetch('/history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
        }})
            .then(response => response.json())
            .then(result => {
                const newHistory = [];
                for(const item of result){
                    newHistory.push(
                        // <div id={item['id']}>
                        //     <img src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`}></img>
                        // </div>
                        <div className="card" style={{ width: '18rem' }}>
                            <img className="card-img-top" src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`} alt="Card image cap"></img>
                            <div className="card-body">
                                <p className="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                            </div>
                      </div>
                    );
                }
                updateHistory(newHistory);

    })
},[]);

    return (
        <React.Fragment>
            <div><section className="word-container">{history}</section></div>
        </React.Fragment>
    ); 
}
ReactDOM.render(<History />, document.querySelector('#root'));