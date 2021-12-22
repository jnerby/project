const History = () => {
    const [history, updateHistory] = React.useState([]);
    // console.log('hello');
    React.useEffect(
        fetch('/history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
        }})
            .then(response => response.json())
            .then(result => {
                // console.log('hi');
                const newHistory = [];
                for(const item of result){
                    newHistory.push(
                        <div id={item['id']}>
                            <img src={`https://image.tmdb.org/t/p/w500/${item['poster_path']}`}></img>
                        </div>
                    );
                }
                updateHistory(newHistory);
            }),[]);
    
    return (
        <div><section className="word-container">{history}</section></div>
    ); 
}
ReactDOM.render(<History />, document.querySelector('#root'));